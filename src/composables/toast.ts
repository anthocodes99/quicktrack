import { ref } from 'vue'
import { v4 as uuidv4 } from 'uuid'

interface Toast {
    id: string
    title: string
    message: string
    status: Status
    buttons: ToastButton[]
    opacity: number
    close: () => void
}

interface ToastButton {
    btnText: string
    btnStatus: ToastButtonColor
    btnCb: () => void
}

export enum Status {
    Info = 'text-primary',
    Warning = 'text-warning',
    Danger = 'text-danger',
    Success = 'text-success',
}

export enum ToastButtonColor {
    Info = 'btn-primary',
    Warning = 'btn-warning',
    Danger = 'btn-danger',
    Success = 'btn-sucess',
}

const toasts = ref<Toast[]>([])

function _destroy(id: string) {
    const toast = toasts.value.find((toast) => toast.id == id)
    if (!toast) return
    toast.opacity = 0
    setTimeout(() => {
        const newToasts = toasts.value.filter((toast) => toast.id !== id)
        toasts.value = newToasts
    }, 500)
}

function makeButton(title: string, status: ToastButtonColor, cb: () => void) {
    return { btnText: title, btnStatus: status, btnCb: cb }
}

function _createToast(
    title: string,
    message: string,
    status: Status,
    buttons: ToastButton[]
) {
    const id = uuidv4()
    const close = function () {
        _destroy(id)
    }
    const toast = {
        id,
        title,
        message,
        status,
        buttons,
        opacity: 0,
        close,
    }
    toasts.value.push(toast)

    // toast.show()
    setTimeout(() => {
        const toast = toasts.value.find((toast) => toast.id == id)
        if (toast) toast.opacity = 100
    }, 100)

    // toast.destroy()
    setTimeout(() => {
        _destroy(id)
    }, 5000)
    return toast
}

function info(title: string, message: string, buttons: ToastButton[] = []) {
    _createToast(title, message, Status.Info, buttons)
}

function warning(title: string, message: string, buttons: ToastButton[] = []) {
    _createToast(title, message, Status.Warning, buttons)
}

/**
 * Sends a Toast with Green Title
 * @param title Title of the Toast
 * @param message Message for the Toast
 */
function success(title: string, message: string, buttons: ToastButton[] = []) {
    _createToast(title, message, Status.Success, buttons)
}

function error(title: string, message: string, buttons: ToastButton[] = []) {
    _createToast(title, message, Status.Danger, buttons)
}

function clearToasts() {
    toasts.value = []
}

export function useToast() {
    const state = {
        // we can't send toasts.value
        // as it will lose reactivity
        toasts,
    }
    return {
        state,
        info,
        warning,
        success,
        error,
        makeButton,
        clearToasts,
    }
}
