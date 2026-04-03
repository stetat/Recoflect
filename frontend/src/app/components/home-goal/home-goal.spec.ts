import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeGoal } from './home-goal';

describe('HomeGoal', () => {
  let component: HomeGoal;
  let fixture: ComponentFixture<HomeGoal>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeGoal]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeGoal);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
