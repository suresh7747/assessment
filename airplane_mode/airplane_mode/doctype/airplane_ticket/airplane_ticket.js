// Copyright (c) 2025, suresh and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Airplane Ticket", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Airplane Ticket', {
  refresh(frm) {
    frm.add_custom_button('Assign Seat', () => {
      const d = new frappe.ui.Dialog({
        title: 'Enter Seat Number',
        fields: [
          {
            label: 'Seat Number',
            fieldname: 'seat_number',
            fieldtype: 'Data',
            reqd: true
          }
        ],
        primary_action_label: 'Assign',
        primary_action(values) {
          frm.set_value('seat', values.seat_number);
          d.hide();
        }
      });
      d.show();
    });
    frm.add_custom_button('change_rate',() =>{
      frappe.prompt({
        fieldname:"rate",
        label:"Rate",
        fieldtype:"float",
        reqd:1,
      },(data)=> {
        frm.set_value("total_amount",data.rate)
        frm.save()
      })
    })
  }
});

frappe.ui.form.on('Add Ons', {
  item(frm,cdt,cdn){
    console.log(cdt,cdn)
  }
})
