import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddGoal } from './add-goal-btn';

describe('AddGoal', () => {
  let component: AddGoal;
  let fixture: ComponentFixture<AddGoal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AddGoal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddGoal);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
