import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SafeCrackerService, CrackSafeResponse } from '../services/safe-cracker.service';

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

      const combinationValue = this.safeCrackerForm.value.combination;

      this.safeCrackerService.crackSafe(combinationValue).subscribe({
        next: (response) => {
          this.result = response;
          this.isLoading = false;
        },
        error: (err) => {
          this.error = 'Failed to crack safe. Please try again.';
          console.error('Error:', err);
          this.isLoading = false;
        }
      });
    }
  }

  onReset(): void {
    this.safeCrackerForm.reset();
    this.result = null;
    this.error = null;
  }
}
