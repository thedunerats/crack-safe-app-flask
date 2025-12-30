import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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
  private apiUrl = 'http://localhost:5000/api/crack_safe/';

  constructor(private http: HttpClient) { }

  crackSafe(combination: string): Observable<CrackSafeResponse> {
    const payload: CrackSafeRequest = {
      actual_combination: combination
    };
    return this.http.post<CrackSafeResponse>(this.apiUrl, payload);
  }
}
