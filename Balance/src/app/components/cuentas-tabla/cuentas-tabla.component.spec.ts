import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CuentasTablaComponent } from './cuentas-tabla.component';

describe('CuentasTablaComponent', () => {
  let component: CuentasTablaComponent;
  let fixture: ComponentFixture<CuentasTablaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CuentasTablaComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CuentasTablaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
