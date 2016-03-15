import { Component, View } from 'angular2/core';
import { Router, RouterLink } from 'angular2/router';
import { CORE_DIRECTIVES, FORM_DIRECTIVES, Validators } from 'angular2/common';
import { Http, Headers } from 'angular2/http';
import {MATERIAL_DIRECTIVES, MATERIAL_PROVIDERS, Media, SidenavService} from "ng2-material/all";
import { contentHeaders } from '../common/headers';

@Component({
  selector: 'login'
})
@View({
  directives: [RouterLink, CORE_DIRECTIVES, MATERIAL_DIRECTIVES, FORM_DIRECTIVES],
  templateUrl: 'app/authentication/login.html',
  styleUrls: ['app/authentication/login.css']
})
export class Login {
  constructor(public router: Router, public http: Http) {
  }

  login(event, email, password) {
    event.preventDefault();
    let body = JSON.stringify({ email, password });
    this.http.post('/api/token-auth/', body, { headers: contentHeaders })
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

  signup(event) {
    event.preventDefault();
    this.router.parent.navigateByUrl('/signup');
  }
}
