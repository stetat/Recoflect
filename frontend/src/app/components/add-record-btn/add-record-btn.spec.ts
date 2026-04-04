import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddRecordBtn } from './add-record-btn';

describe('AddRecordBtn', () => {
  let component: AddRecordBtn;
  let fixture: ComponentFixture<AddRecordBtn>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddRecordBtn]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddRecordBtn);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
