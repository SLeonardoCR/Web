import { Component, OnInit, Input } from '@angular/core';
import { Cuenta, Cuentas } from 'src/app/models/Cuentas';

@Component({
  selector: 'app-cuentas-tabla',
  templateUrl: './cuentas-tabla.component.html',
  styleUrls: ['./cuentas-tabla.component.scss']
})
export class CuentasTablaComponent implements OnInit {
  cuentas: Cuenta[] = [];
  estadoCuentas = '';
  mostrarAgregar = false;
  mostrarEditar = false;
  nuevaCuenta = {
    numero: '',
    tipo: '',
    nombre: '',
    cantidad: 0
  };
  editarContenidoCuenta = {
    numero: '',
    tipo: '',
    nombre: '',
    cantidad: 0
  };
  restarCuenta = {
    cuenta1: '',
    cuenta2: '',
    cantidad: 0
  };

  constructor(private cuentasService: Cuentas) { }

  ngOnInit(): void {
    this.cuentas = this.cuentasService.getCuentas();
    this.cuadra();
  }

  mostrarFormulario(eleccion: string) {
    if (eleccion==='editar')
      this.mostrarEditar = !this.mostrarEditar;
    if (eleccion==='agregar')
      this.mostrarAgregar = !this.mostrarAgregar;
    
  }

  agregarCuenta() {
    this.cuentas.push(this.nuevaCuenta);
    this.nuevaCuenta = {
      numero: '',
      tipo: '',
      nombre: '',
      cantidad: 0
    };
    this.mostrarAgregar = false;
    this.cuadra();
  }
  eliminarCuenta(index: number): void
  {
    this.cuentas.splice(index, 1);
    localStorage.setItem("cuentas", JSON.stringify(this.cuentas));
    this.cuadra();
  }
  cuentasTipoActivo() {
    return this.cuentas.filter(cuenta => cuenta.tipo === 'Activo');
  }
  cuentasTipoPasivo() {
    return this.cuentas.filter(cuenta => cuenta.tipo === 'Pasivo' || cuenta.tipo === 'Capital');
  }

  editarCuenta(): void{
    const cons = this.cuentas.findIndex(cuenta => cuenta.numero === this.editarContenidoCuenta.numero); 
    this.cuentas[cons].cantidad = this.editarContenidoCuenta.cantidad;
    this.cuentas[cons].nombre = this.editarContenidoCuenta.nombre;
    this.cuentas[cons].tipo = this.editarContenidoCuenta.tipo;
    localStorage.setItem('cuentas', JSON.stringify(this.cuentas));
  }

  restarCantidad(cantidad: number, nombreCuenta1: string, nombreCuenta2: string) {
    const cuenta1 = this.cuentas.find(cuenta => cuenta.nombre === nombreCuenta1);
    const cuenta2 = this.cuentas.find(cuenta => cuenta.nombre === nombreCuenta2);

    if (!cuenta1 || !cuenta2) {
      console.error('Una o ambas cuentas no existen');
      return;
    }

    if (cuenta1.cantidad < cantidad) {
      console.error(`La cantidad en la cuenta ${cuenta1.nombre} es insuficiente`);
      return;
    }

    cuenta1.cantidad -= cantidad;
    cuenta2.cantidad -= cantidad;

    localStorage.setItem('cuentas', JSON.stringify(this.cuentas));
    this.cuadra();
  }

  restarCuentas() {
    this.restarCantidad(this.restarCuenta.cantidad, this.restarCuenta.cuenta1, this.restarCuenta.cuenta2)
    this.restarCuenta = {
      cuenta1: '',
      cuenta2: '',
      cantidad: 0
    };
    this.cuentas = this.cuentasService.getCuentas();
    this.cuadra();
  }

  cuadra() {
    let sumaHaber = 0;
    let sumaDebe = 0;
    for (const cuenta of this.cuentas) {
      if (cuenta.tipo === 'Activo') {
        sumaDebe += cuenta.cantidad;
      }
      else {
        sumaHaber += cuenta.cantidad;
      }
    }
    if (sumaDebe === sumaHaber)
      this.estadoCuentas = 'Cuadra';
    else
      this.estadoCuentas = 'No cuadra';
    console.log(this.estadoCuentas);
  }

}
