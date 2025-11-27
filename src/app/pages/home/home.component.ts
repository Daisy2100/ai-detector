import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AiDetectorService, DetectionResult } from '../../services/ai-detector.service';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  inputText: string = '';
  isLoading: boolean = false;
  result: DetectionResult | null = null;
  errorMessage: string = '';

  constructor(private aiDetectorService: AiDetectorService) {}

  get wordCount(): number {
    return this.inputText.trim().split(/\s+/).filter(word => word.length > 0).length;
  }

  get characterCount(): number {
    return this.inputText.length;
  }

  detectText(): void {
    if (!this.inputText || this.inputText.trim().length < 50) {
      this.errorMessage = 'Please enter at least 50 characters for accurate analysis.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';
    this.result = null;

    this.aiDetectorService.detectText(this.inputText).subscribe({
      next: (response) => {
        this.result = response;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.error || 'An error occurred while analyzing the text.';
        this.isLoading = false;
      }
    });
  }

  clearText(): void {
    this.inputText = '';
    this.result = null;
    this.errorMessage = '';
  }

  getResultClass(): string {
    if (!this.result) return '';
    switch (this.result.prediction) {
      case 'AI':
        return 'result-ai';
      case 'Human':
        return 'result-human';
      default:
        return 'result-uncertain';
    }
  }

  getProgressBarColor(): string {
    if (!this.result) return '#3b82f6';
    if (this.result.ai_probability > 60) return '#ef4444';
    if (this.result.human_probability > 60) return '#22c55e';
    return '#f59e0b';
  }
}
