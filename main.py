from log_singleton import Log

log1 = Log()
log2 = Log()

log1.create_log("Payment", "Customer payment completed")
log2.create_log("Inqury", "Customer inquiry submitted")

print(log1.view_logs())
print(log2.view_logs())

print(log1 is log2)

