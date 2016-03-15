import { bootstrap } from 'angular2/platform/browser';
import { provide } from 'angular2/core';
import { FORM_PROVIDERS } from 'angular2/common';
import { ROUTER_PROVIDERS } from 'angular2/router';
import { LocationStrategy} from 'angular2/router';
import { HashLocationStrategy} from 'angular2/router';
import { Http, HTTP_PROVIDERS } from 'angular2/http';
import { AuthConfig, AuthHttp } from 'angular2-jwt';

import {GestaoLivreApp} from './app/gestaolivre';

bootstrap(
    GestaoLivreApp,
    [
        FORM_PROVIDERS,
        ROUTER_PROVIDERS,
        HTTP_PROVIDERS,
        provide(AuthHttp, {
            useFactory: (http) => {
                return new AuthHttp(new AuthConfig({}), http);
            },
            deps: [Http]
        }),
        provide(LocationStrategy, {
          useClass: HashLocationStrategy
        }),
    ]
);
