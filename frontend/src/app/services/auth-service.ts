import {Injectable, signal} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Router} from '@angular/router';
import {Observable, tap} from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api';
  private accessKey = 'auth_token';
  private refreshKey = 'refresh_token';
  firstName = signal<string | null>(localStorage.getItem('firstName'));
  isLoggedIn = signal<boolean>(this.checkInitialLoginState());
  constructor(private http: HttpClient, private router: Router) { }

  register(userData: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/register/`, userData).pipe(
      tap(res => {
        this.setAccessToken(res.access);
        this.setRefreshToken(res['refresh']);
        this.isLoggedIn.set(true);
      })
    )
  }

  login(credentials: any): Observable<any> {
    return this.http.post<{access: string, refresh: string, first_name: string}>(`${this.apiUrl}/login/`, credentials).pipe(
      tap(res => {
        this.setAccessToken(res.access);
        this.setRefreshToken(res['refresh']);
        localStorage.setItem('firstName', res.first_name);
        this.firstName.set(res.first_name);
        this.isLoggedIn.set(true);
      })
    )
  }

  logout(): void {
    localStorage.removeItem(this.accessKey);
    localStorage.removeItem(this.refreshKey);
    localStorage.removeItem('first_name');
    this.isLoggedIn.set(false);
    void this.router.navigate(['login']);
  }

  refreshToken(token: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/token/refresh/`, {refresh: token}).pipe(
      tap(res => {
        this.setAccessToken(res.access);

        if(res.refresh) {
          this.setRefreshToken(res.refresh);
        }
      })
    );
  }

  public setAccessToken(token: string): void {
    localStorage.setItem(this.accessKey, token);
  }

  public getToken(): string | null {
  return localStorage.getItem(this.accessKey);
  }

  public setRefreshToken(refreshToken: string): void {
    localStorage.setItem(this.refreshKey, refreshToken);
  }

  public getRefreshToken(): string | null {
    return localStorage.getItem(this.refreshKey);
  }

  private checkInitialLoginState(): boolean {
    return localStorage.getItem(this.accessKey) !== null;
  }


  private getName() {
    return this.http.get<String>(`${this.apiUrl}/getName/`)
  }
}
