import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SafeCrackerService, CrackSafeResponse, ProgressUpdate } from './safe-cracker.service';
import { environment } from '../../environments/environment';

describe('SafeCrackerService', () => {
  let service: SafeCrackerService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SafeCrackerService]
    });
    service = TestBed.inject(SafeCrackerService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  describe('crackSafe', () => {
    it('should be created', () => {
      expect(service).toBeTruthy();
    });

    it('should make POST request to crack safe endpoint', () => {
      const combination = '1234567890';
      const mockResponse: CrackSafeResponse = {
        attempts: 55,
        time_taken: 12.34
      };

      service.crackSafe(combination).subscribe(response => {
        expect(response).toEqual(mockResponse);
        expect(response.attempts).toBe(55);
        expect(response.time_taken).toBe(12.34);
      });

      const req = httpMock.expectOne(`${environment.apiUrl}/api/crack_safe/`);
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toEqual({ actual_combination: combination });
      expect(req.request.headers.get('X-API-Key')).toBe(environment.apiKey);
      expect(req.request.headers.get('Content-Type')).toBe('application/json');

      req.flush(mockResponse);
    });

    it('should include API key in headers', () => {
      const combination = '0000000000';

      service.crackSafe(combination).subscribe();

      const req = httpMock.expectOne(`${environment.apiUrl}/api/crack_safe/`);
      expect(req.request.headers.has('X-API-Key')).toBe(true);
      expect(req.request.headers.get('X-API-Key')).toBe(environment.apiKey);

      req.flush({ attempts: 10, time_taken: 1.0 });
    });

    it('should handle error responses', () => {
      const combination = '1234567890';
      const errorMessage = 'Unauthorized';

      service.crackSafe(combination).subscribe({
        next: () => fail('should have failed with 401 error'),
        error: (error) => {
          expect(error.status).toBe(401);
        }
      });

      const req = httpMock.expectOne(`${environment.apiUrl}/api/crack_safe/`);
      req.flush(errorMessage, { status: 401, statusText: 'Unauthorized' });
    });

    it('should send correct payload structure', () => {
      const combination = '9999999999';

      service.crackSafe(combination).subscribe();

      const req = httpMock.expectOne(`${environment.apiUrl}/api/crack_safe/`);
      expect(req.request.body).toEqual({
        actual_combination: combination
      });

      req.flush({ attempts: 100, time_taken: 20.0 });
    });
  });

  describe('crackSafeWithProgress', () => {
    it('should handle streaming progress updates', (done) => {
      const combination = '1234567890';
      const progressUpdates: ProgressUpdate[] = [];
      
      // Mock fetch for streaming
      const mockResponse = `{"type":"progress","attempts":10,"current_attempt":"1000000000","correct_digits":1,"total_digits":10}
{"type":"progress","attempts":20,"current_attempt":"1200000000","correct_digits":2,"total_digits":10}
{"type":"complete","attempts":55,"time_taken":12.34}
`;

      spyOn(window, 'fetch').and.returnValue(
        Promise.resolve(new Response(mockResponse, {
          status: 200,
          headers: { 'Content-Type': 'application/x-ndjson' }
        }))
      );

      service.crackSafeWithProgress(
        combination,
        (progress: ProgressUpdate) => {
          progressUpdates.push(progress);
        }
      ).then((result) => {
        expect(progressUpdates.length).toBe(2);
        expect(progressUpdates[0].attempts).toBe(10);
        expect(progressUpdates[1].attempts).toBe(20);
        expect(result.type).toBe('complete');
        expect(result.attempts).toBe(55);
        expect(result.time_taken).toBe(12.34);
        done();
      });
    });

    it('should call progress callback for each update', (done) => {
      const combination = '0000000000';
      let callCount = 0;
      
      const mockResponse = `{"type":"progress","attempts":10,"current_attempt":"0000000000","correct_digits":4,"total_digits":10}
{"type":"progress","attempts":20,"current_attempt":"0000000000","correct_digits":4,"total_digits":10}
{"type":"progress","attempts":30,"current_attempt":"0000000000","correct_digits":4,"total_digits":10}
{"type":"complete","attempts":34,"time_taken":5.0}
`;

      spyOn(window, 'fetch').and.returnValue(
        Promise.resolve(new Response(mockResponse, { status: 200 }))
      );

      service.crackSafeWithProgress(
        combination,
        () => { callCount++; }
      ).then(() => {
        expect(callCount).toBe(3);
        done();
      });
    });

    it('should include API key in fetch headers', () => {
      const combination = '1234567890';
      const fetchSpy = spyOn(window, 'fetch').and.returnValue(
        Promise.resolve(new Response('{"type":"complete","attempts":1,"time_taken":0.1}', { status: 200 }))
      );

      service.crackSafeWithProgress(combination, () => {});

      expect(fetchSpy).toHaveBeenCalledWith(
        `${environment.apiUrl}/api/crack_safe/stream`,
        jasmine.objectContaining({
          method: 'POST',
          headers: jasmine.objectContaining({
            'X-API-Key': environment.apiKey
          })
        })
      );
    });

    it('should handle fetch errors', (done) => {
      const combination = '1234567890';
      
      spyOn(window, 'fetch').and.returnValue(
        Promise.reject(new Error('Network error'))
      );

      service.crackSafeWithProgress(
        combination,
        () => {}
      ).catch((error) => {
        expect(error.message).toBe('Network error');
        done();
      });
    });

    it('should handle non-OK response status', (done) => {
      const combination = '1234567890';
      
      spyOn(window, 'fetch').and.returnValue(
        Promise.resolve(new Response('', { status: 401, statusText: 'Unauthorized' }))
      );

      service.crackSafeWithProgress(
        combination,
        () => {}
      ).catch((error) => {
        expect(error.message).toContain('401');
        done();
      });
    });

    it('should parse progress updates correctly', (done) => {
      const combination = '5555555555';
      let receivedProgress: ProgressUpdate | null = null;
      
      const mockResponse = `{"type":"progress","attempts":40,"current_attempt":"5555555555","correct_digits":10,"total_digits":10}
{"type":"complete","attempts":45,"time_taken":8.5}
`;

      spyOn(window, 'fetch').and.returnValue(
        Promise.resolve(new Response(mockResponse, { status: 200 }))
      );

      service.crackSafeWithProgress(
        combination,
        (progress: ProgressUpdate) => {
          receivedProgress = progress;
        }
      ).then(() => {
        expect(receivedProgress).not.toBeNull();
        expect(receivedProgress?.type).toBe('progress');
        expect(receivedProgress?.attempts).toBe(40);
        expect(receivedProgress?.current_attempt).toBe('5555555555');
        expect(receivedProgress?.correct_digits).toBe(10);
        expect(receivedProgress?.total_digits).toBe(10);
        done();
      });
    });
  });
});
