import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface DetectionResult {
  prediction: 'AI' | 'Human' | 'Uncertain' | 'Unknown';
  confidence: number;
  ai_probability: number;
  human_probability: number;
  word_count?: number;
  features?: {
    avg_sentence_length?: number;
    vocabulary_richness?: number;
    formality_score?: number;
  };
  message: string;
}

export interface DetectionError {
  error: string;
}

@Injectable({
  providedIn: 'root'
})
export class AiDetectorService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  /**
   * Detect if text is AI-generated or human-written
   * @param text The text to analyze
   * @returns Observable<DetectionResult>
   */
  detectText(text: string): Observable<DetectionResult> {
    return this.http.post<DetectionResult>(this.apiUrl, { text }).pipe(
      catchError(error => {
        console.error('AI Detection error:', error);
        return throwError(() => error.error || { error: 'An error occurred while analyzing the text.' });
      })
    );
  }
}
