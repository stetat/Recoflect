import { Component, inject } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth-service';

@Component({
  selector: 'app-navigation',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navigation.html',
  styleUrl: './navigation.css',
})
export class Navigation {
  private authService: AuthService = inject(AuthService);

  logOut(): void {
    this.authService.logout();
    this.isLoggedIn.set(false);
  }

  isLoggedIn = this.authService.isLoggedIn;
}