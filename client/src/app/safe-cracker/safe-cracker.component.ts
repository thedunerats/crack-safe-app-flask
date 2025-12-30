import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SafeCrackerService, CrackSafeResponse, ProgressUpdate } from '../services/safe-cracker.service';

@Component({
  selector: 'app-safe-cracker',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './safe-cracker.component.html',
  styleUrl: './safe-cracker.component.css'
})
export class SafeCrackerComponent {
  safeCrackerForm: FormGroup;
  result: CrackSafeResponse | null = null;
  isLoading = false;
  error: string | null = null;
  
  // Real-time progress tracking
  currentAttempts = 0;
  currentProgress: ProgressUpdate | null = null;

  constructor(
    private fb: FormBuilder,
    private safeCrackerService: SafeCrackerService
  ) {
    this.safeCrackerForm = this.fb.group({
      combination: ['', [
        Validators.required,
        Validators.pattern(/^\d{10}$/),
        Validators.minLength(10),
        Validators.maxLength(10)
      ]]
    });
  }

  get combination() {
    return this.safeCrackerForm.get('combination');
  }

  onSubmit(): void {
    if (this.safeCrackerForm.valid) {
      this.isLoading = true;
      this.error = null;
      this.result = null;
      this.currentAttempts = 0;
      this.currentProgress = null;

      const combinationValue = this.safeCrackerForm.value.combination;

      // Use streaming endpoint for real-time progress
      this.safeCrackerService.crackSafeWithProgress(
        combinationValue,
        (progress: ProgressUpdate) => {
          // Update progress in real-time
          this.currentAttempts = progress.attempts;
          this.currentProgress = progress;
        }
      ).then((finalResult) => {
        // Set final result
        this.result = {
          attempts: finalResult.attempts,
          time_taken: finalResult.time_taken
        };
        this.isLoading = false;
        this.currentProgress = null;
      }).catch((err) => {
        this.error = 'Failed to crack safe. Please try again.';
        console.error('Error:', err);
        this.isLoading = false;
        this.currentProgress = null;
      });
    }
  }

  onReset(): void {
    this.safeCrackerForm.reset();
    this.result = null;
    this.error = null;
    this.currentAttempts = 0;
    this.currentProgress = null;
  }
}
