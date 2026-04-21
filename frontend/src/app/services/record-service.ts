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

export interface Category {
  id: string;
  title: string;
}

export interface CreateRecordPayload {
  type: 1 | 2;
  category: string;
  amount: number;
  date: string;
  reflection: 1 | 2 | 3;
}

@Injectable({
  providedIn: 'root',
})
export class RecordService {
  private apiUrl = 'http://localhost:8000/api/records/';
  private categoriesUrl = 'http://localhost:8000/api/categories/';

  constructor(private http: HttpClient) {}

  getRecords(): Observable<RecordItem[]> {
    return this.http.get<RecordItem[]>(this.apiUrl);
  }

  createRecord(data: CreateRecordPayload): Observable<RecordItem> {
    return this.http.post<RecordItem>(this.apiUrl, data);
  }

  deleteRecord(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }

  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.categoriesUrl);
  }

  createCategory(title: string): Observable<Category> {
    return this.http.post<Category>(this.categoriesUrl, { title });
  }
}
