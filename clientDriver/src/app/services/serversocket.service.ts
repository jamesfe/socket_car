import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { Subscription } from 'rxjs/Subscription';
import { Observable } from 'rxjs/Observable';
import { Observer } from 'rxjs/Observer';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/filter';
import 'rxjs/add/observable/dom/webSocket';

const DRIVER_URL = 'ws://localhost:8080/blah';

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
        this.ws = Observable.webSocket(DRIVER_URL);
        this.messages = makeHot(this.ws).map(parseFrame).filter(m => m != null);
    }

    sendGenMessage(msg: GenMessage) {
        let frame: Frame = {
            type: 'GenMessage',
            data: {
                body: msg.body,
            },
        };
        this.ws.next(JSON.stringify(frame));
    }

}

function parseFrame(frame: Frame): Message {
    if (frame.type === 'GenMessage') {
        let msg = new GenMessage();
        msg.body = frame.data.body;
        return msg;
    }
    return null;
}

function makeHot<T>(cold: Observable<T>): Observable<T> {
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