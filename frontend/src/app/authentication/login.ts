import { Component, View } from 'angular2/core';
import { Router, RouterLink } from 'angular2/router';
import { CORE_DIRECTIVES, Validators } from 'angular2/common';
import { FORM_DIRECTIVES, FormBuilder, ControlGroup, AbstractControl } from 'angular2/common';
import {NgFormModel} from 'angular2/common';
import { Http, Headers } from 'angular2/http';
import { MATERIAL_DIRECTIVES, MATERIAL_PROVIDERS, Media, SidenavService} from "ng2-material/all";
import { contentHeaders } from '../common/headers';
import { ValidationService } from '../common/ValidationService';

export class Login {
  constructor(
    public email : string,
    public password : string
  ) { }
}

@Component({
  selector: 'login-form',
  templateUrl: '/app/authentication/login-form.component.html',
  directives: [RouterLink, CORE_DIRECTIVES, MATERIAL_DIRECTIVES, FORM_DIRECTIVES]
})
export class LoginFormComponent {
  model = new Login('', '');
  submitted = false;

  constructor(public router: Router, public http: Http) {
  }

  onSubmit(): void {
    let body = JSON.stringify({ email: this.model.email, password: this.model.password });

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

  get diagnostic() { return JSON.stringify(this.model); }
}


@Component({
  selector: 'login',
  template: '<login-form></login-form>',
  directives: [LoginFormComponent]
})
export class LoginComponent {
  constructor(public router: Router, public http: Http) {
  }

  signup(event) {
    event.preventDefault();
    this.router.parent.navigateByUrl('/signup');
  }
}
