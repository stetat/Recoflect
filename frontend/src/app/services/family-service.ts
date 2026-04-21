import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface FamilyMember {
  id: string;
  username: string;
  first_name: string;
  role: 1 | 2 | 3;
  weekly_income: number;
  weekly_expense: number;
  limit: number | null;
}

export interface FamilyJoinRequest {
  id: string;
  username: string;
  first_name: string;
  desired_role: 1 | 2 | 3;
  status: 1 | 2 | 3;
  created_at: string;
}

export interface FamilyData {
  id: string;
  family_name: string;
  invite_code: string;
  members: FamilyMember[];
  current_user_role: 1 | 2 | 3 | null;
  current_user_id: string | null;
  join_requests: FamilyJoinRequest[];
}

export interface FamilyResponse {
  family: FamilyData | null;
  pending_join_request?: FamilyJoinRequest | null;
}

export interface FamilyJoinResponse {
  detail: string;
  pending_join_request: FamilyJoinRequest;
}

@Injectable({
  providedIn: 'root',
})
export class FamilyService {
  private apiUrl = 'http://localhost:8000/api/family/';

  constructor(private http: HttpClient) {}

  getFamily(): Observable<FamilyData | FamilyResponse> {
    return this.http.get<FamilyData | FamilyResponse>(this.apiUrl);
  }

  createFamily(family_name: string): Observable<FamilyData> {
    return this.http.post<FamilyData>(`${this.apiUrl}create/`, { family_name });
  }

  joinFamily(invite_code: string, desired_role: 1 | 2): Observable<FamilyJoinResponse> {
    return this.http.post<FamilyJoinResponse>(`${this.apiUrl}join/`, {
      invite_code,
      desired_role,
    });
  }

  regenerateInviteCode(): Observable<FamilyData> {
    return this.http.post<FamilyData>(`${this.apiUrl}regenerate-invite/`, {});
  }

  removeMember(member_id: string): Observable<FamilyData> {
    return this.http.post<FamilyData>(`${this.apiUrl}remove-member/`, { member_id });
  }

  leaveFamily(): Observable<FamilyResponse> {
    return this.http.post<FamilyResponse>(`${this.apiUrl}leave/`, {});
  }

  approveRequest(requestId: string): Observable<FamilyData> {
    return this.http.post<FamilyData>(`${this.apiUrl}requests/${requestId}/approve/`, {});
  }

  rejectRequest(requestId: string): Observable<FamilyData> {
    return this.http.post<FamilyData>(`${this.apiUrl}requests/${requestId}/reject/`, {});
  }
}
