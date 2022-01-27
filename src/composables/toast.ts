import { ref } from 'vue'
import { v4 as uuidv4 } from 'uuid'

interface toast {
    id: string
    title: string
    message: string
    status: Status
    opacity: number
    close: () => void
}

export enum Status {
    Info = 'text-primary',
    Warning = 'text-warning',
    Danger = 'text-danger',
    Success = 'text-success',
}

const toasts = ref<toast[]>([])

function _destroy(id: string) {
    const toast = toasts.value.find((toast) => toast.id == id)
    if (!toast) return
    toast.opacity = 0
    setTimeout(() => {
        const newToasts = toasts.value.filter((toast) => toast.id !== id)
        toasts.value = newToasts
    }, 500)
}

function _createToast(title: string, message: string, status: Status) {
    const id = uuidv4()
    const close = function () {
        _destroy(id)
    }
    const toast = {
        id,
        title,
        message,
        status,
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

function info(title: string, message: string) {
    _createToast(title, message, Status.Info)
}

function warning(title: string, message: string) {
    _createToast(title, message, Status.Warning)
}

/**
 * Sends a Toast with Green Title
 * @param title Title of the Toast
 * @param message Message for the Toast
 */
function success(title: string, message: string) {
    _createToast(title, message, Status.Success)
}

function error(title: string, message: string) {
    _createToast(title, message, Status.Danger)
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
        clearToasts,
    }
}
