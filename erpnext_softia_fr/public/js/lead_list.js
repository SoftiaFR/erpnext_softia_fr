frappe.listview_settings['Lead'] = {
    hide_name_column: true,
    
    onload: function(listview) {
        hide_like_column();
        
        const original_render = listview.render_list;
        listview.render_list = function() {
            original_render.call(this);
            add_custom_columns(listview);
        };
        
        add_custom_columns(listview);
    },
    
    refresh: function(listview) {
        hide_like_column();
        add_custom_columns(listview);
    },
};

function add_custom_columns(listview) {
    setTimeout(function() {
        // Utilise la structure interne de Frappe
        const $page = listview.$page;
        const $result = $page.find('.result');

        // Injecte un style minimal une seule fois pour afficher un aperçu clamped
        if (!document.getElementById('custom-task-style')) {
            var css = '\n                .list-row-col.custom-task-desc .ellipsis{ display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; text-overflow:ellipsis; max-width:150px; }\n                .list-row-col.custom-task-desc .ellipsis[title]{ cursor:help; }\n                .list-row-col.custom-task-desc{ min-width:150px; }\n            ';
            var style = document.createElement('style');
            style.id = 'custom-task-style';
            style.appendChild(document.createTextNode(css));
            document.head.appendChild(style);
        }
        
        
        // Ajoute les headers
        const $header = $result.find('.list-row-head');
        if ($header.length && $header.find('.custom-task-date-header').length === 0) {
            $header.find('.list-row-col:first').after(`
                <div class="list-row-col custom-task-desc-header ellipsis" style="flex: 0 0 150px; max-width: 150px;">
                    <span class="ellipsis">${__("Last Task Description")}</span>
                </div>
                <div class="list-row-col custom-task-date-header ellipsis" style="flex: 0 0 150px; max-width: 150px;">
                    <span class="ellipsis">${__("Last Task Date")}</span>
                </div>
                <div class="list-row-col custom-task-assigned-header ellipsis" style="flex: 0 0 150px; max-width: 150px;">
                    <span class="ellipsis">${__("Last Task Assignee")}</span>
                </div>
            `);
        }
        
        // Boucle sur listview.data 
        listview.data.forEach(function(row_data, idx) {
            const lead_name = row_data.name;
            
            // Cherche la row par index dans le DOM
            const $rows = $result.find('.list-row:not(.list-row-head)');
            const $row = $rows.eq(idx);
            
            if ($row.length === 0) {
                return;
            }
            
            // Skip si déjà traité
            if ($row.find('.custom-task-date').length > 0) {
                return;
            }
            
            const $firstCol = $row.find('.list-row-col:first');
            
            if ($firstCol.length === 0) return;
            
            // Crée les colonnes
            const $desc_col = $(`
                <div class="list-row-col custom-task-desc ellipsis" style="flex: 0 0 150px; max-width: 150px;">
                    <span class="ellipsis">...</span>
                </div>
            `);
            const $date_col = $(`
                <div class="list-row-col custom-task-date ellipsis" style="flex: 0 0 150px; max-width: 150px;">
                    <span class="ellipsis">...</span>
                </div>
            `);
            const $assign_col = $(`
                <div class="list-row-col custom-task-assigned ellipsis" style="flex: 0 0 150px; max-width: 150px;">
                    <span class="ellipsis">...</span>
                </div>
            `);
            
            $firstCol.after($assign_col).after($date_col).after($desc_col);
            
            // Appel API
            frappe.call({
                method: "erpnext_softia_fr.api.todo.get_last_task_info", 
                args: { lead_name: lead_name },
                callback: function(r) {
                    if (r.message && r.message.date) {
                        // Date et assigné en texte simple
                        $date_col.find('span').text(r.message.date).attr('title', r.message.date);
                        $assign_col.find('span').text(r.message.assigned_to).attr('title', r.message.assigned_to);

                        // La description peut contenir du HTML (Quill). On nettoie pour afficher
                        var plain = '';
                        try {
                            plain = $('<div>').html(r.message.description).text().trim();
                        } catch (e) {
                            plain = String(r.message.description || '');
                        }

                        if (plain.length === 0) {
                            $desc_col.find('span').text('—').removeAttr('title');
                        } else {
                            $desc_col.find('span').text(plain).attr('title', plain);
                        }
                    } else {
                        $desc_col.find('span').text('—');
                        $date_col.find('span').text('—');
                        $assign_col.find('span').text('—');
                    }
                }
            });
        });
    }, 100);
}

function hide_like_column() {
    setTimeout(function() {
        $('span.level-item.list-liked-by-me.hidden-xs').remove();
        $('span.list-row-like.hidden-xs').remove();
        $('span.comment-count.d-flex.align-items-center').remove();
        $('span.mx-2').remove();

        $('.level-right').remove();      
    }, 50);
}
