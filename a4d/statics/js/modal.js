class Modal {
    constructor(settings) {
        /* Settings:
        * modal <- required
        * onShow
        * onHide
        * onAccept
        * onDeny
        * */
        this.settings = settings;
        if (!settings.modal) {
            console.error('No modal object is given');
            return;
        }
        this.modal = settings.modal;
        if (this.modal.find('.close').length > 0) {
            this.modal.find('.close').on('click', () => {
                this.close()
            });
        }
        if (this.modal.find('.accept').length > 0 && settings.onAccept) {
            this.modal.find('.accept').on('click', () => {
                var result = this.settings.onAccept(this);
                if (result || result === undefined) {
                    this.close()
                }
            });
        }
        if (this.modal.find('.deny').length > 0) {
            this.modal.find('.deny').on('click', () => {
                var result = undefined;
                if (this.settings.onDeny) {
                    result = this.settings.onDeny(this);
                }
                if (result || result === undefined) {
                    this.close()
                }
            });
        }


    }

    disable_buttons() {
        var deny_found = this.modal.find('.deny')
        if (deny_found.length > 0) {
            deny_found.attr('disabled', true).addClass('disabled');
        }
        var accept_found = this.modal.find('.accept')
        if (accept_found.length > 0) {
            accept_found.attr('disabled', true).addClass('disabled');
        }
    }

    enable_buttons() {
        var deny_found = this.modal.find('.deny')
        if (deny_found.length > 0) {
            deny_found.attr('disabled', false).removeClass('disabled');
        }
        var accept_found = this.modal.find('.accept')
        if (accept_found.length > 0) {
            accept_found.attr('disabled', false).removeClass('disabled');
        }
    }

    show() {
        var result = undefined;
        if (this.settings.onShow) {
            result = this.settings.onShow(this);
        }
        if (result || result === undefined) {
            this.modal.css('display', 'block');
        }
    }

    close() {
        var result = undefined;
        if (this.settings.onHide) {
            result = this.settings.onHide(this);
        }
        if (result || result === undefined) {
            this.modal.css('display', 'none');
        }
    }
}
