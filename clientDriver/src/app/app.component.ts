import { Component, OnInit } from "@angular/core";
import { HostListener } from '@angular/core';

import { SocketService, Message } from './services/serversocket.service';


@Component({
    selector: "socketcar",
    styleUrls: [ "./app.component.scss" ],
    templateUrl: "./app.component.html",
    providers: [ SocketService ]
})

export class AppComponent implements OnInit {
    private turnval = 5; // how fast do we turn?
    private speedinc = 5; // how fast do we turn?

    public constructor(private controlService: SocketService) {}

    public ngOnInit(): void {}

    @HostListener('document:keypress', ['$event'])
    handleKeyboardEvent(event: KeyboardEvent) {
      var message: Message;
      console.log(event.key);
      switch(event.key) {
          case 'a':
            console.log("faster");
            message = {purpose: "speed", left: true, right: true, value: this.speedinc};
            break;
          case 'z':
             console.log("erroneous msg");
             message = {purpose: "zoozie"};
             break;
      }
      console.log("Sending keypress..." + message);
    }

}