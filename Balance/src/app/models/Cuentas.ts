import { Injectable } from '@angular/core';

export interface Cuenta {
  numero: string;
  tipo: string;
  nombre: string;
  cantidad: number;
}
@Injectable({
  providedIn: 'root',
})
export class Cuentas {
  public cuentas: Cuenta[] = [];

  constructor() {
    const storedCuentas = localStorage.getItem('cuentas');
    if (storedCuentas) {
      this.cuentas = JSON.parse(storedCuentas);
    }
  }

  public crearCuenta(cuenta: Cuenta) {
    this.cuentas.push(cuenta);
    this.guardarCuentas();
  }

  public getCuentas(): Cuenta[] {
    return this.cuentas;
  }

  public getCuenta(numero: string): Cuenta | undefined {
    return this.cuentas.find(cuenta => cuenta.numero === numero);
  }

  public modificarCuenta(numero: string, nuevaCantidad: number) {
    const cuenta = this.getCuenta(numero);
    if (cuenta) {
      cuenta.cantidad = nuevaCantidad;
      this.guardarCuentas();
    }
  }

  private guardarCuentas() {
    localStorage.setItem('cuentas', JSON.stringify(this.cuentas));
  }
}