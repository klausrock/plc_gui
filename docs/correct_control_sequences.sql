def motor_auto_setup(ctx: 'Context'):
    """Determine motor parameters and store them on the device.

    :param ctx: menu context
    """
    ctx.wait_for_user_confirmation = True

    if ctx.active_device == None:
        handle_error_message(ctx, "", "No active device set. Select an active device first.")
        return

    print("\n" + ctx.light_yellow)
    print("Please note the following requirements for performing the auto-setup:")
    print("- The motor must be unloaded.")
    print("- The motor must not be touched.")
    print("- The motor must be able to rotate freely in any direction.")
    print("- No NanoJ program may be running." + ctx.def_color)

    result = input("Do you want to continue? [y/n]: ")
    if result.lower() != "y":
        return

    # Stop a possibly running NanoJ program
    write_result: Nanolib.ResultVoid = ctx.nanolib_accessor.writeNumber(ctx.active_device, 0x00, OdIndex.odNanoJControl,
                                                                        32)
    if write_result.hasError():
        handle_error_message(ctx, "Error during motor_auto_setup: ", write_result.getError())
        return

    # Switch the state machine to "voltage enabled"
    write_result: Nanolib.ResultVoid = ctx.nanolib_accessor.writeNumber(ctx.active_device, 0x06, OdIndex.odControlWord,
                                                                        16)
    if write_result.hasError():
        handle_error_message(ctx, "Error during motor_auto_setup: ", write_result.getError())
        return

    # Set mode of operation to auto-setup
    write_result: Nanolib.ResultVoid = ctx.nanolib_accessor.writeNumber(ctx.active_device, 0xFE,
                                                                        OdIndex.odModeOfOperation, 8)
    if write_result.hasError():
        handle_error_message(ctx, "Error during motor_auto_setup: ", write_result.getError())
        return

    # Switch on
    write_result: Nanolib.ResultVoid = ctx.nanolib_accessor.writeNumber(ctx.active_device, 0x07, OdIndex.odControlWord,
                                                                        16)
    if write_result.hasError():
        handle_error_message(ctx, "Error during motor_auto_setup: ", write_result.getError())
        return

    # Switch the state machine to "enable operation"
    write_result: Nanolib.ResultVoid = ctx.nanolib_accessor.writeNumber(ctx.active_device, 0x0F, OdIndex.odControlWord,
                                                                        16)
    if write_result.hasError():
        handle_error_message(ctx, "Error during motor_auto_setup: ", write_result.getError())
        return

    # Run auto setup
    write_result: Nanolib.ResultVoid = ctx.nanolib_accessor.writeNumber(ctx.active_device, 0x1F, OdIndex.odControlWord,
                                                                        16)
    if write_result.hasError():
        handle_error_message(ctx, "Error during motor_auto_setup: ", write_result.getError())
        return

    print("Motor auto setup is running, please wait ...")

    # Wait until auto setup is finished, check status word
    while True:
        read_number_result: Nanolib.ResultInt = ctx.nanolib_accessor.readNumber(ctx.active_device, OdIndex.odStatusWord)
        if read_number_result.hasError():
            handle_error_message(ctx, "Error during motor_auto_setup: ", read_number_result.getError())
            return

        # Finish if bits 12, 9, 5, 4, 2, 1, 0 are set
        if (read_number_result.getResult() & 0x1237) == 0x1237:
            break

    # Reboot current active device
    print("Rebooting ...")
    reboot_result: Nanolib.ResultVoid = ctx.nanolib_accessor.rebootDevice(ctx.active_device)
    if reboot_result.hasError():
        handle_error_message(ctx, "Error during motor_auto_setup: ", reboot_result.getError())
        return
    print("Motor auto setup finished.")