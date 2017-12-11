import { Component, OnInit } from "@angular/core";
import { HostListener } from '@angular/core';

import { SocketService, Message } from './services/serversocket.service';


@Component({
    selector: "client-car-main",
    styleUrls: [ "./app.component.scss" ],
    templateUrl: "./app.component.html",
    providers: [ SocketService ]
})

export class ClientCarMainComponent implements OnInit {
    private turnval = 5; // how fast do we turn?
    private speedinc = 5; // how fast do we turn?

    public constructor(private controlService: SocketService) {}

    public ngOnInit(): void {}

    @HostListener('document:keypress', ['$event'])
    handleKeyboardEvent(event: KeyboardEvent) {
        /* We capture all the keypresses so the app can control the car when the screen is 
        in focus. */
        let validKeys = "basdfqwz12345";
        if (validKeys.indexOf(event.key) !== -1) {
            this.controlService.sendMessageBasedOnEvent(event.key);
        }
    }

}