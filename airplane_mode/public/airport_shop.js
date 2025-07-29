frappe.ui.form.on('Airport Shop', {
  setup(frm) {
    frm.set_query('shop_type', () => {
      return {
        filters: {
          enabled: 1
        }
      };
    });
  }
});
