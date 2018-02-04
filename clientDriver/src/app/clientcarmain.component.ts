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
        let validKeys = "bsfqwz12345";
        if (validKeys.indexOf(event.key) !== -1) {
            this.controlService.sendMessageBasedOnEvent(event.key);
        }
    }

    @HostListener('document:keydown', ['$event'])
    handleKeyDown(event: KeyboardEvent) {
        /* We only send turn messages while the key is held down, after that it
        raises to send the car in a straight line again. (handleKeyUp resets) */
        let validKeys = "ad";
        if (validKeys.indexOf(event.key) !== -1) {
            this.controlService.sendMessageBasedOnEvent(event.key);
        }
    }

    @HostListener('document:keyup', ['$event'])
    handleKeyUp(event: KeyboardEvent) {
        /* If the user lets go of a turning key, we send a message to zero the servo. */
        let validKeys = "ad";
        if (validKeys.indexOf(event.key) !== -1) {
            this.controlService.sendMessageBasedOnEvent('â');
        }
    }

}
