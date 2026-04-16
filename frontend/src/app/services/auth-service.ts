import {Injectable, signal} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {Observable, tap} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api';
  private tokenKey = 'auth_token';

  constructor(private http: HttpClient, private router: Router) { }

  login(credentials: any): Observable<any> {
    return this.http.post<{token: string}>(`${this.apiUrl}/login/`, credentials).pipe(
      tap(res => {
        this.setToken(res.token);
        this.isLoggedIn.set(true);
      })
    )
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    this.isLoggedIn.set(false);
    void this.router.navigate(['login']);
  }

  public setToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  public getToken(): string | null {
  return localStorage.getItem(this.tokenKey);
  }

  private checkInitialLoginState(): boolean {
    return localStorage.getItem(this.tokenKey) !== null;
  }

  public isLoggedIn = signal<boolean>(this.checkInitialLoginState());

}
