import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  nombre = 'Leonardo Rangel';
  textPlaceholder="Escribe algo aquí";
  texto="Esto es un video / boton sobre event binding"
  texto2="";
  //objeto
  listEstudiantes: any[]= [
   {no_control:"1914", nombreAlumno:"Juan Pablo",semestre:"VIII"},
    {no_control:"8414", nombreAlumno:"Pedro Celestino",semestre:"VIII"},
    {no_control:"0314", nombreAlumno:"Julio Cesar",semestre:"VIII"},
    
  ]
  constructor()
  {
    setInterval( ()=> this.nombre = 'Programación Web',3000);
  }
  //practica 2
  cambiarText():void{
    this.texto="en el proximo video vamos a ver two way data-binding";
  }
   mostrar = true;
   toogle():void
   {
    this.mostrar =!this.mostrar
   }
}
