import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable';
import { Observer } from 'rxjs/Observer';

import 'rxjs/add/operator/map';
import 'rxjs/add/observable/dom/webSocket';

const DRIVER_URL = 'ws://localhost:9001/control_socket';

export interface Message {
    purpose: string,
	direction?: string,
    value?: number,
    left?: boolean,
    right?: boolean,
    message?: string,
    type?: string,
    time?: number,
    health_check?: any
}

export interface HealthCheck {
    left_motor: number,
    right_motor: number,
    steering: number
  }

Injectable()
export class SocketService {
    // Cheers! From: https://github.com/PeterKassenaar/ng2-websockets/
    public messages: Subject<Message>  = new Subject<Message>();
    private turnval = 5; // how fast do we turn?
    private speedinc = 5; // how fast do we turn?

    constructor() {
        this.messages = <Subject<Message>>this.connect()
            .map((response: MessageEvent): Message => {
                let data = JSON.parse(response.data);
                let p = {
                    purpose : data.purpose,
                    direction: data.direction,
                    value: data.value,
                    left: data.left,
                    right: data.right,
                    message: data.message,
                    type: data.type,
                    time: data.time,
                    health_check: data.health_check
                }
                return p;
            });
    }

  private socket: Subject<MessageEvent>;
  url: string = DRIVER_URL;

  public connect(): Subject<MessageEvent> {
    if(!this.socket) {
      this.socket = this.create(this.url);
    }
    return this.socket;
  }

  public sendMessageBasedOnEvent(event: String) {
      var message: Message;
      switch (event) {
        case "badEvent":
        case "b":
          message = {purpose: "blah"}
          break;
        case "left":
        case "a":
          message = {purpose: "turn", direction: "left", value: this.turnval}
          break;
        case "right":
        case "d":
          message = {purpose: "turn", direction: "right", value: this.turnval}
          break;
        case "incspeed":
        case "w":
          message = {purpose: "speed", left: true, right: true, value: this.speedinc}
          break;
        case "decspeed":
        case "s":
          message = {purpose: "speed", left: true, right: true, value: -1 * this.speedinc}
          break;
        case "zero":
        case "z":
          message = {purpose: "zero"}
          break;
        case "stop":
        case "q":
          message = {purpose: "stop"}
          break;
        case "1":
        case "2":
        case "3":
        case "4":
        case "5":
            message = {purpose: "shift", value: parseInt(event.toString())}
        default:
          console.log("Did not receive a valid action.");
      }
      if (message) {
        this.messages.next(message);
      } else {
        console.log("message not valid, did not send.");
      }
  }

  private create(url: string): Subject<MessageEvent> {
    let ws = new WebSocket(url);
    let observable = Observable.create(
        (obs: Observer<MessageEvent>) => {
            ws.onmessage = obs.next.bind(obs);
            ws.onerror = obs.error.bind(obs);
            ws.onclose = obs.complete.bind(obs);
            return ws.close.bind(ws);
        }
    );
    let observer = {
        next: (data: Object) => {
            if (ws.readyState === WebSocket.OPEN) {
                // console.log("Sending some data.", data);
                ws.send(JSON.stringify(data));
            }
        },
    };
    return Subject.create(observer, observable);
  }

}
