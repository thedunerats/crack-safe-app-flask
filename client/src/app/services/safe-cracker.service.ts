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

@Injectable({
  providedIn: 'root'
})
export class SafeCrackerService {
  private apiUrl = `${environment.apiUrl}/api/crack_safe/`;
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
}
