import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddRecordForm } from './add-record-form';

describe('AddRecordForm', () => {
  let component: AddRecordForm;
  let fixture: ComponentFixture<AddRecordForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddRecordForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddRecordForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
