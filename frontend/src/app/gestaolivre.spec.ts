import {describe, it, expect, beforeEachProviders, inject} from 'angular2/testing';
import {GestaoLivreApp} from '../app/gestaolivre';

beforeEachProviders(() => [GestaoLivreApp]);

/*
describe('App: Gestaolivre', () => {
  it('should have the `defaultMeaning` as 42', inject([GestaoLivreApp], (app: GestaoLivreApp) => {
    expect(app.defaultMeaning).toBe(42);
  }));

  describe('#meaningOfLife', () => {
    it('should get the meaning of life', inject([GestaoLivreApp], (app: GestaoLivreApp) => {
      expect(app.meaningOfLife()).toBe('The meaning of life is 42');
      expect(app.meaningOfLife(22)).toBe('The meaning of life is 22');
    }));
  });
});
*/
