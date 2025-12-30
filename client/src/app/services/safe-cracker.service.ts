import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface CrackSafeResponse {
  attempts: number;
  time_taken: number;
}

export interface CrackSafeRequest {
  actual_combination: string;
}

export interface ProgressUpdate {
  type: 'progress';
  attempts: number;
  current_attempt: string;
  correct_digits: number;
  total_digits: number;
}

export interface CompleteUpdate {
  type: 'complete';
  attempts: number;
  time_taken: number;
}

export type StreamUpdate = ProgressUpdate | CompleteUpdate;

@Injectable({
  providedIn: 'root'
})
export class SafeCrackerService {
  private apiUrl = `${environment.apiUrl}/api/crack_safe/`;
  private streamApiUrl = `${environment.apiUrl}/api/crack_safe/stream`;
  private apiKey = environment.apiKey;

  constructor(private http: HttpClient) { }

  crackSafe(combination: string): Observable<CrackSafeResponse> {
    const payload: CrackSafeRequest = {
      actual_combination: combination
    };
    
    // Add API key to request headers
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'X-API-Key': this.apiKey
    });
    
    return this.http.post<CrackSafeResponse>(this.apiUrl, payload, { headers });
  }

  /**
   * Crack safe with real-time progress updates using streaming
   * @param combination The combination to crack
   * @param onProgress Callback function called with each progress update
   * @returns Promise that resolves with the final result
   */
  crackSafeWithProgress(
    combination: string,
    onProgress: (progress: ProgressUpdate) => void
  ): Promise<CompleteUpdate> {
    return new Promise((resolve, reject) => {
      const payload: CrackSafeRequest = {
        actual_combination: combination
      };

      // Use fetch API for streaming support
      fetch(this.streamApiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': this.apiKey
        },
        body: JSON.stringify(payload)
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          if (!response.body) {
            throw new Error('Response body is null');
          }

          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let buffer = '';

          const readStream = () => {
            reader.read().then(({ done, value }) => {
              if (done) {
                return;
              }

              // Decode the chunk and add to buffer
              buffer += decoder.decode(value, { stream: true });

              // Process complete lines (NDJSON format)
              const lines = buffer.split('\n');
              buffer = lines.pop() || ''; // Keep incomplete line in buffer

              for (const line of lines) {
                if (line.trim()) {
                  try {
                    const update: StreamUpdate = JSON.parse(line);
                    
                    if (update.type === 'progress') {
                      onProgress(update);
                    } else if (update.type === 'complete') {
                      resolve(update);
                      return;
                    }
                  } catch (e) {
                    console.error('Error parsing JSON:', e);
                  }
                }
              }

              // Continue reading
              readStream();
            }).catch(error => {
              reject(error);
            });
          };

          readStream();
        })
        .catch(error => {
          reject(error);
        });
    });
  }
}

