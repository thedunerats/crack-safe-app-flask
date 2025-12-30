import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { SafeCrackerComponent } from './safe-cracker/safe-cracker.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, SafeCrackerComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'Safe Cracker App';
}
