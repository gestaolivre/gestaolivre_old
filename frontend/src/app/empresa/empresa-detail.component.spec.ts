import {
  it,
  iit,
  describe,
  ddescribe,
  expect,
  inject,
  injectAsync,
  TestComponentBuilder,
  beforeEachProviders
} from 'angular2/testing';
import {provide} from 'angular2/core';
import {EmpresaDetailComponent} from './empresa-detail.component';
import {Router, RouteParams} from 'angular2/router';
import {Empresa, EmpresaService} from './empresa.service';

class MockEmpresaService {
  get() { return Promise.resolve(new Empresa('10711130000196', 'GINX LTDA -ME', 'GINX')); }
}

class MockRouter {
  navigate() { }
}

class MockRouteParams {
  get() { return 1; }
}

describe('EmpresaDetailComponent', () => {

  beforeEachProviders(() => [
    provide(EmpresaService, {useClass: MockEmpresaService}),
    provide(Router, {useClass: MockRouter}),
    provide(RouteParams, {useClass: MockRouteParams}),
  ]);

  it('should ...', injectAsync([TestComponentBuilder], (tcb:TestComponentBuilder) => {
    return tcb.createAsync(EmpresaDetailComponent).then((fixture) => {
      fixture.detectChanges();
    });
  }));

});
