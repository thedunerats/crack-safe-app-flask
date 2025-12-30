import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { SafeCrackerComponent } from './safe-cracker.component';
import { SafeCrackerService, CrackSafeResponse, ProgressUpdate, CompleteUpdate } from '../services/safe-cracker.service';
import { of, throwError } from 'rxjs';

describe('SafeCrackerComponent', () => {
  let component: SafeCrackerComponent;
  let fixture: ComponentFixture<SafeCrackerComponent>;
  let mockService: jasmine.SpyObj<SafeCrackerService>;

  beforeEach(async () => {
    // Create mock service
    mockService = jasmine.createSpyObj('SafeCrackerService', ['crackSafe', 'crackSafeWithProgress']);

    await TestBed.configureTestingModule({
      imports: [SafeCrackerComponent, ReactiveFormsModule],
      providers: [
        { provide: SafeCrackerService, useValue: mockService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(SafeCrackerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('Form Validation', () => {
    it('should initialize with an empty form', () => {
      expect(component.safeCrackerForm.value.combination).toEqual('');
    });

    it('should require combination field', () => {
      const control = component.combination;
      expect(control?.valid).toBeFalsy();
      expect(control?.errors?.['required']).toBeTruthy();
    });

    it('should validate exactly 10 digits', () => {
      const control = component.combination;
      
      // Test invalid lengths
      control?.setValue('123');
      expect(control?.valid).toBeFalsy();
      
      control?.setValue('12345678901'); // 11 digits
      expect(control?.valid).toBeFalsy();
      
      // Test valid 10 digits
      control?.setValue('1234567890');
      expect(control?.valid).toBeTruthy();
    });

    it('should only accept numeric characters', () => {
      const control = component.combination;
      
      control?.setValue('123456789a');
      expect(control?.valid).toBeFalsy();
      
      control?.setValue('123 456 789');
      expect(control?.valid).toBeFalsy();
      
      control?.setValue('1234567890');
      expect(control?.valid).toBeTruthy();
    });

    it('should validate pattern /^\\d{10}$/', () => {
      const control = component.combination;
      
      control?.setValue('0000000000');
      expect(control?.valid).toBeTruthy();
      
      control?.setValue('9999999999');
      expect(control?.valid).toBeTruthy();
      
      control?.setValue('abcdefghij');
      expect(control?.valid).toBeFalsy();
    });
  });

  describe('Form Submission', () => {
    it('should not submit if form is invalid', () => {
      component.safeCrackerForm.controls['combination'].setValue('123');
      component.onSubmit();
      
      expect(mockService.crackSafeWithProgress).not.toHaveBeenCalled();
    });

    it('should call crackSafeWithProgress on valid submission', () => {
      const mockComplete: CompleteUpdate = {
        type: 'complete',
        attempts: 55,
        time_taken: 12.34
      };
      
      mockService.crackSafeWithProgress.and.returnValue(Promise.resolve(mockComplete));
      
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.onSubmit();
      
      expect(mockService.crackSafeWithProgress).toHaveBeenCalledWith(
        '1234567890',
        jasmine.any(Function)
      );
    });

    it('should set loading state during submission', () => {
      const mockComplete: CompleteUpdate = {
        type: 'complete',
        attempts: 55,
        time_taken: 12.34
      };
      
      mockService.crackSafeWithProgress.and.returnValue(Promise.resolve(mockComplete));
      
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      
      expect(component.isLoading).toBeFalsy();
      component.onSubmit();
      expect(component.isLoading).toBeTruthy();
    });

    it('should reset state on submission', () => {
      const mockComplete: CompleteUpdate = {
        type: 'complete',
        attempts: 55,
        time_taken: 12.34
      };
      
      mockService.crackSafeWithProgress.and.returnValue(Promise.resolve(mockComplete));
      
      component.result = { attempts: 100, time_taken: 20 };
      component.error = 'Previous error';
      component.currentAttempts = 50;
      
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.onSubmit();
      
      expect(component.result).toBeNull();
      expect(component.error).toBeNull();
      expect(component.currentAttempts).toBe(0);
    });

    it('should update result on successful completion', (done) => {
      const mockComplete: CompleteUpdate = {
        type: 'complete',
        attempts: 55,
        time_taken: 12.34
      };
      
      mockService.crackSafeWithProgress.and.returnValue(Promise.resolve(mockComplete));
      
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.onSubmit();
      
      setTimeout(() => {
        expect(component.result).toEqual({
          attempts: 55,
          time_taken: 12.34
        });
        expect(component.isLoading).toBeFalsy();
        done();
      }, 10);
    });

    it('should handle errors during submission', (done) => {
      mockService.crackSafeWithProgress.and.returnValue(
        Promise.reject(new Error('Network error'))
      );
      
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.onSubmit();
      
      setTimeout(() => {
        expect(component.error).toBe('Failed to crack safe. Please try again.');
        expect(component.isLoading).toBeFalsy();
        done();
      }, 10);
    });
  });

  describe('Progress Tracking', () => {
    it('should update currentAttempts during progress', (done) => {
      const mockProgress: ProgressUpdate = {
        type: 'progress',
        attempts: 30,
        current_attempt: '1230000000',
        correct_digits: 3,
        total_digits: 10
      };
      
      const mockComplete: CompleteUpdate = {
        type: 'complete',
        attempts: 55,
        time_taken: 12.34
      };
      
      let progressCallback: ((progress: ProgressUpdate) => void) | null = null;
      
      mockService.crackSafeWithProgress.and.callFake((combination: string, onProgress: (p: ProgressUpdate) => void) => {
        progressCallback = onProgress;
        return Promise.resolve(mockComplete);
      });
      
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.onSubmit();
      
      setTimeout(() => {
        if (progressCallback) {
          progressCallback(mockProgress);
          expect(component.currentAttempts).toBe(30);
          expect(component.currentProgress).toEqual(mockProgress);
        }
        done();
      }, 10);
    });

    it('should clear progress after completion', (done) => {
      const mockComplete: CompleteUpdate = {
        type: 'complete',
        attempts: 55,
        time_taken: 12.34
      };
      
      mockService.crackSafeWithProgress.and.returnValue(Promise.resolve(mockComplete));
      
      component.currentProgress = {
        type: 'progress',
        attempts: 40,
        current_attempt: '1234000000',
        correct_digits: 4,
        total_digits: 10
      };
      
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.onSubmit();
      
      setTimeout(() => {
        expect(component.currentProgress).toBeNull();
        done();
      }, 10);
    });

    it('should initialize currentAttempts to 0', () => {
      expect(component.currentAttempts).toBe(0);
    });

    it('should initialize currentProgress to null', () => {
      expect(component.currentProgress).toBeNull();
    });
  });

  describe('Reset Functionality', () => {
    it('should reset form on reset', () => {
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.onReset();
      
      expect(component.safeCrackerForm.value.combination).toBeNull();
    });

    it('should clear result on reset', () => {
      component.result = { attempts: 55, time_taken: 12.34 };
      component.onReset();
      
      expect(component.result).toBeNull();
    });

    it('should clear error on reset', () => {
      component.error = 'Some error';
      component.onReset();
      
      expect(component.error).toBeNull();
    });

    it('should clear progress tracking on reset', () => {
      component.currentAttempts = 40;
      component.currentProgress = {
        type: 'progress',
        attempts: 40,
        current_attempt: '1234000000',
        correct_digits: 4,
        total_digits: 10
      };
      
      component.onReset();
      
      expect(component.currentAttempts).toBe(0);
      expect(component.currentProgress).toBeNull();
    });

    it('should reset all state', () => {
      // Set all state
      component.safeCrackerForm.controls['combination'].setValue('1234567890');
      component.result = { attempts: 55, time_taken: 12.34 };
      component.error = 'Error message';
      component.currentAttempts = 50;
      component.currentProgress = {
        type: 'progress',
        attempts: 50,
        current_attempt: '1234567000',
        correct_digits: 7,
        total_digits: 10
      };
      
      // Reset
      component.onReset();
      
      // Verify all cleared
      expect(component.safeCrackerForm.value.combination).toBeNull();
      expect(component.result).toBeNull();
      expect(component.error).toBeNull();
      expect(component.currentAttempts).toBe(0);
      expect(component.currentProgress).toBeNull();
    });
  });

  describe('Combination Getter', () => {
    it('should return combination form control', () => {
      const control = component.combination;
      expect(control).toBeTruthy();
      expect(control).toBe(component.safeCrackerForm.get('combination'));
    });
  });

  describe('UI State Management', () => {
    it('should disable submit button when form is invalid', () => {
      component.safeCrackerForm.controls['combination'].setValue('123');
      fixture.detectChanges();
      
      const button = fixture.nativeElement.querySelector('button[type="submit"]');
      expect(button.disabled).toBeTruthy();
    });

    it('should disable buttons when loading', () => {
      component.isLoading = true;
      fixture.detectChanges();
      
      const submitButton = fixture.nativeElement.querySelector('button[type="submit"]');
      const resetButton = fixture.nativeElement.querySelector('button[type="button"]');
      
      expect(submitButton.disabled).toBeTruthy();
      expect(resetButton.disabled).toBeTruthy();
    });

    it('should show loading text when loading', () => {
      component.isLoading = true;
      fixture.detectChanges();
      
      const buttonText = fixture.nativeElement.querySelector('button[type="submit"]').textContent;
      expect(buttonText).toContain('Cracking...');
    });

    it('should show normal text when not loading', () => {
      component.isLoading = false;
      fixture.detectChanges();
      
      const buttonText = fixture.nativeElement.querySelector('button[type="submit"]').textContent;
      expect(buttonText).toContain('Crack Safe');
    });
  });
});
