import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ControlStickComponent } from './control-stick.component';

describe('ControlStickComponent', () => {
  let component: ControlStickComponent;
  let fixture: ComponentFixture<ControlStickComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ControlStickComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ControlStickComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
