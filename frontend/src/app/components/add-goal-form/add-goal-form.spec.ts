import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddGoalForm } from './add-goal-form';

describe('AddGoalForm', () => {
  let component: AddGoalForm;
  let fixture: ComponentFixture<AddGoalForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddGoalForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddGoalForm);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
