import {View, Component} from 'angular2/core';
import { CORE_DIRECTIVES } from 'angular2/common';
import { Http, Headers } from 'angular2/http';
import {Location, RouteConfig, RouterLink, Router} from 'angular2/router';
import {AuthHttp, JwtHelper} from 'angular2-jwt';

import {Observable} from 'rxjs/Rx';

import {LoggedInRouterOutlet} from './LoggedInOutlet';
import {Home} from './home/home';
import {Login} from './authentication/login';
import {Signup} from './authentication/signup';
import {contentHeaders} from './common/headers';
import {EmpresaRoot} from './empresa/empresa-root.component';

@Component({
  selector: 'gestaolivre-app'
})
@View({
  templateUrl: './app/gestaolivre.html',
  directives: [LoggedInRouterOutlet, CORE_DIRECTIVES]
})
@RouteConfig([
  { path: '/', redirectTo: ['/Home'] },
  { path: '/home', component: Home, as: 'Home' },
  { path: '/login', component: Login, as: 'Login' },
  { path: '/signup', component: Signup, as: 'Signup' },
  { path: '/empresa/...', component: EmpresaRoot, as: 'Empresa' }
])
export class GestaoLivreApp {
  tokenExpires: number;
  tokenExpired: boolean;

  constructor(public router: Router, public http: Http, public authHttp: AuthHttp) {
    let timer = Observable.timer(2000, 1000);
    let jwtHelper: JwtHelper = new JwtHelper();
    timer.subscribe(t => {
      var token = jwtHelper.decodeToken(localStorage.getItem('id_token'));
      if (token) {
        this.tokenExpires = ((token.exp * 1000) - Number(new Date()));
        this.tokenExpired = this.tokenExpires <= 0;
        if (this.tokenExpires > -5000 && this.tokenExpires < 2000) {
          this.refreshToken();
        }
      }
    });
  }

  refreshToken() {
    let token = localStorage.getItem('id_token');
    let body = JSON.stringify({ token: token });
    this.http.post('/api/token-refresh/', body, { headers: contentHeaders })
      .subscribe(
        response => {
          localStorage.setItem('id_token', response.json().token);
          this.router.parent.navigateByUrl('/home');
        },
        error => {
          alert(error.text());
          console.log(error.text());
        }
      );
  }
}
