/* Toggle sidebar */
const sidebarToggle = document.querySelector("#sidebar-toggle");
sidebarToggle.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("collapsed");
});

/* Loading Spinner */
const spinnerWrapperEl = document.querySelector('.spinner-wrapper');
window.addEventListener('load', () => {
    spinnerWrapperEl.style.opacity = '0';
    setTimeout(() => {
        spinnerWrapperEl.style.display = 'none';
    }, 200);
});

/* DataTable */
$(document).ready(function () {
    $('#myTable').DataTable();
});

/**/
$(document).ready(function () {
    //Dynamic Row Addition
    $(".add-button").click(function () {
        // Select options from existing select
        const serviceOptions = $(".service-selector").first().html();

        const newRow = `
            <tr>
                <td>
                    <select name="serviceID[]" class="form-control service-selector" required>
                        ${serviceOptions}
                    </select>
                </td>
                <td><input class="form-control" type="text" name="itemDesc[]" placeholder="Service Descriptions" required></td>
                <td><input class="form-control item-price" type="number" name="itemPrice[]" placeholder="Fee" required></td>
                <td><input class="form-control item-qty" type="number" name="itemQty[]" placeholder="Qty" required></td>
                <td><input class="form-control item-amt" type="number" name="itemAmt[]" placeholder="Amount" readonly></td>
                <td><button type="button" class="btn btn-danger remove-button">-</button></td>
            </tr>`;
        $("#dataTable tbody").append(newRow);
    });

    // Remove Row
    $(document).on('click', '.remove-button', function () {
        $(this).closest('tr').remove();
        calculateSubtotal(); // Recalculate everything after removing
    });

    // Auto-fill price when service is selected
    $(document).on('change', '.service-selector', function () {
        const selectedOption = $(this).find('option:selected');
        const fee = selectedOption.data('fee') || 0;
        const row = $(this).closest('tr');

        // Set the price
        row.find('.item-price').val(fee);

        // Calculate row amount
        calculateRowAmount(row);
    });

    // Calculate row amount
    function calculateRowAmount(row) {
        const price = parseFloat(row.find('.item-price').val()) || 0;
        const qty = parseFloat(row.find('.item-qty').val()) || 0;
        const amount = price * qty;

        row.find('input[name="itemAmt[]"]').val(amount.toFixed(2));
        calculateSubtotal();
    }

    // Calculate subtotal
    function calculateSubtotal() {
        let subtotal = 0;
        $('input[name="itemAmt[]"]').each(function () {
            subtotal += parseFloat($(this).val()) || 0;
        });
        $('#invSubtotal').val(subtotal.toFixed(2));
        calculateDue();
    }

    function calculateDue() {
        const subtotal = parseFloat($('#invSubtotal').val()) || 0;
        const paid = parseFloat($('#invPaid').val()) || 0;
        const due = subtotal - paid;
        // Make sure this ID matches your HTML (invTotal)
        $('#invTotal').val(due.toFixed(2));
    }

    // Calculate row based on manual input changes
    $(document).on('input', '.item-price, .item-qty', function () {
        const row = $(this).closest('tr');
        calculateRowAmount(row);
    });

    // Calculate due based on manual input changes
    $(document).on('input', '#invPaid', function () {
        calculateDue();
    });
});