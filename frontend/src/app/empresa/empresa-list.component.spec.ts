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
import {EmpresaListComponent} from './empresa-list.component';
import {Empresa, EmpresaService} from './empresa.service';

class MockEmpresaService {
  getAll() { return Promise.resolve([new Empresa('10711130000196', 'GINX LTDA - ME', 'GINX')]); }
}

describe('EmpresaListComponent', () => {

  beforeEachProviders(() => [
    provide(EmpresaService, {useClass: MockEmpresaService}),
  ]);

  it('should ...', injectAsync([TestComponentBuilder], (tcb:TestComponentBuilder) => {
    return tcb.createAsync(EmpresaListComponent).then((fixture) => {
      fixture.detectChanges();
    });
  }));

});
