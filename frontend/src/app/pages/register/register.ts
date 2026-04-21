import {Component, signal} from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {AuthService} from '../../services/auth-service';
import {Router, RouterLink, RouterLinkActive} from '@angular/router';

@Component({
  selector: 'app-register',
  imports: [
    ReactiveFormsModule,
    RouterLink,
    RouterLinkActive
  ],
  templateUrl: './register.html',
  styleUrl: './register.css',
})
export class Register {
  registerForm: FormGroup;
  errorMessage = signal<string>('');
  hidePassword = signal<boolean>(true);

  constructor (
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.registerForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', [
        Validators.required,
        Validators.minLength(8),
        Validators.pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/)
      ]],
      email: ['', Validators.required],
      first_name: ['', Validators.required],
    });
  }

  togglePassword(){
    this.hidePassword.update(prevState => !prevState);
  }

  onSubmit(){
    if (this.registerForm.valid) {
      this.authService.register(this.registerForm.value).subscribe({
        next: () => {
          this.errorMessage.set('');
          void this.router.navigate(['/home']);
        },
        error: err => {
          const backendError =
            err?.error?.username?.[0] ??
            err?.error?.email?.[0] ??
            err?.error?.password?.[0] ??
            err?.error?.detail ??
            'Registration failed.';

          this.errorMessage.set(backendError);
          console.error(err);
        }
      });
    }
  }

}
