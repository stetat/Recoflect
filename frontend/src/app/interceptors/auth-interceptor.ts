import {HttpHandlerFn, HttpInterceptorFn} from '@angular/common/http';
import {AuthService} from '../services/auth-service';
import {inject} from '@angular/core';
import {catchError, switchMap, throwError} from 'rxjs';


export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const token = authService.getToken();

  let authReq = req;
  if (token) {
    authReq = addTokenHeader(req, token);
  }

  return next(authReq).pipe(
    catchError((err) => {
      if (err.status === 401 && token) {
        return handle401Error(authReq, next, authService);
      }
      return throwError(() => err);
    })
  );

  function addTokenHeader(req: any, token: string) {
    return req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    })
  }

  function handle401Error(req: any, next: HttpHandlerFn, authService: AuthService) {
    const refreshToken = authService.getRefreshToken();
    if (!refreshToken) {
      authService.logout();
      return throwError(() => new Error('no refresh token available'));

    }

    return authService.refreshToken(refreshToken).pipe(
      switchMap((res: any) => {
        authService.setAccessToken(res.access);
        return next(addTokenHeader(req, res.access));

      }),
      catchError((refreshErr) => {
        authService.logout();
        return throwError(() => new Error('no refresh token available'));
      })
    );
  }

};
