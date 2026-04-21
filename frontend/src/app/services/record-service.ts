import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RecordItem {
  id: string;
  type: 1 | 2;
  category: string;
  category_title: string;
  amount: string;
  date: string;
  reflection: 1 | 2 | 3;
}

@Injectable({
  providedIn: 'root',
})
export class RecordService {
  private apiUrl = 'http://localhost:8000/api/records/';

  constructor(private http: HttpClient) {}

  getRecords(): Observable<RecordItem[]> {
    return this.http.get<RecordItem[]>(this.apiUrl);
  }

  deleteRecord(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }
}
