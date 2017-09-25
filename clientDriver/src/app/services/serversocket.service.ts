import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable';
import { Observer } from 'rxjs/Observer';

import 'rxjs/add/operator/map';
import 'rxjs/add/observable/dom/webSocket';

const DRIVER_URL = 'ws://localhost:9001/control_socket';

export interface Message {
	purpose: string,
	message: string,
}

Injectable()
export class SocketService {
    // Cheers! From: https://github.com/PeterKassenaar/ng2-websockets/
    public messages: Subject<Message>  = new Subject<Message>();

    constructor() {
        this.messages = <Subject<Message>>this.connect()
            .map((response: MessageEvent): Message => {
                let data = JSON.parse(response.data);
                return {
                    purpose : data.purpose,
                    message: data.message
                }
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
                ws.send(JSON.stringify(data));
            }
        },
    };
    return Subject.create(observer, observable);
  }

}
