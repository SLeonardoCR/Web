import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'piano';
  aplicarSonido(numero:number): void
  {
    let audio = new Audio();
    switch (numero)
    {
      case 1: 
        audio.src="../assets/sonidos/c.mp3"; 
        audio.load();
        audio.play();break
      case 2:
        audio.src="../assets/sonidos/d.mp3"; 
        audio.load();
        audio.play();break
      case 3:
        audio.src="../assets/sonidos/e.mp3"; 
        audio.load();
        audio.play();break
      case 4:
        audio.src="../assets/sonidos/f.mp3"; 
        audio.load();
        audio.play();break
      case 5:
        audio.src="../assets/sonidos/g.mp3"; 
        audio.load();
        audio.play();break
      case 6:
        audio.src="../assets/sonidos/a.mp3"; 
        audio.load();
        audio.play();break
      case 7:
        audio.src="../assets/sonidos/b.mp3"; 
        audio.load();
        audio.play();break
    }
    
  }
}
