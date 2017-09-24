import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Subscription } from 'rxjs/Subscription';
import { Observable } from 'rxjs/Observable';
import { Observer } from 'rxjs/Observer';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';
import 'rxjs/add/observable/dom/webSocket';

const DRIVER_URL = 'ws://localhost:9001/control_socket';

export interface Message {
    toString(): string;
}

export class GenMessage implements Message {
    body: string;

    toString(): string {
        return "blah";
    }
}

interface Frame {
    type: string;
    data: any;
};

@Injectable()
export class SocketService {
    public messages: Observable<Message>;
    private ws: Subject<any>;

    constructor() {
        console.log("Constructing web socket");
        this.ws = Observable.webSocket(DRIVER_URL);
        this.messages = makeHot(this.ws).map(parseFrame).filter(m => m != null);
        console.log("WS Constructed. ", this.ws);
    }

    sendGenMessage(msg: GenMessage) {
        console.log("Sending message!", this.ws);
        let frame: Frame = {
            type: 'GenMessage',
            data: {
                body: msg.body,
            },
        };
        console.log("sending frame");
        this.ws.next(JSON.stringify(frame));
    }

}

function parseFrame(frame: Frame): Message {
    console.log("Parsing frame.");
    if (frame.type === 'GenMessage') {
        let msg = new GenMessage();
        msg.body = frame.data.body;
        return msg;
    } else {
        console.log(frame);
    }
    return null;
}

function makeHot<T>(cold: Observable<T>): Observable<T> {
    console.log("Making it hot.");
    let subject = new Subject();
    let refs = 0;
    return Observable.create((observer: Observer<T>) => {
        let coldSub: Subscription;
        if (refs === 0) {
            coldSub = cold.subscribe(o => subject.next(o));
        }
        refs++;
        let hotSub = subject.subscribe(observer);
        return () => {
            refs--;
            if (refs === 0) {
                coldSub.unsubscribe();
            }
            hotSub.unsubscribe();
        };
    });
}