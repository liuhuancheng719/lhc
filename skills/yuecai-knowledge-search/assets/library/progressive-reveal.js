/* Progressive Reveal · zero-dependency global API */
(function (window, document) {
  'use strict';

  const ROOT_SELECTOR = '[data-progressive-reveal]';
  const ITEM_SELECTOR = '[data-reveal="item"]';
  const REPLAY_SELECTOR = '[data-reveal-replay]';

  function resolveRoot(root) {
    const element = typeof root === 'string' ? document.querySelector(root) : root;
    if (!(element instanceof HTMLElement)) {
      throw new TypeError('ProgressiveReveal.init(root) expects an HTMLElement or selector.');
    }
    return element;
  }

  function init(root) {
    const element = resolveRoot(root);

    if (element.__progressiveReveal) {
      return element.__progressiveReveal;
    }

    const replay = () => {
      element.classList.remove('is-animating');
      void element.offsetWidth;
      element.classList.add('is-animating');
    };

    element.querySelectorAll(ITEM_SELECTOR).forEach((item, index) => {
      if (!item.style.getPropertyValue('--reveal-delay')) {
        item.style.setProperty('--reveal-delay', item.dataset.delay || `${index * 90 + 220}ms`);
      }
    });

    const replayButtons = [...element.querySelectorAll(REPLAY_SELECTOR)];
    replayButtons.forEach((button) => button.addEventListener('click', replay));

    const instance = {
      root: element,
      replay,
      destroy() {
        replayButtons.forEach((button) => button.removeEventListener('click', replay));
        delete element.__progressiveReveal;
      },
    };

    element.__progressiveReveal = instance;
    replay();
    return instance;
  }

  function autoInit() {
    document.querySelectorAll(ROOT_SELECTOR).forEach(init);
  }

  window.ProgressiveReveal = {
    init,
    autoInit,
    replay(root) {
      return init(root).replay();
    },
  };

  autoInit();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoInit, { once: true });
  }
}(window, document));
