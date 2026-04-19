import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeRecords } from './home-records';
import { RouterLink } from '@angular/router';
 describe('HomeRecords', () => {
  let component: HomeRecords;
  let fixture: ComponentFixture<HomeRecords>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HomeRecords]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HomeRecords);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
