from datetime import datetime

def reestructurar_cadena(data, id):
    created_at = datetime.now()
    transformed_data = {
        "created_date": created_at.strftime("%Y-%m-%d"),
        "created_time": created_at.strftime("%H:%M:%S"),
        "id_user": id,
        "length": len(data),
        "data": data,
    }
    return transformed_data

class DataEcgResponse():

    @staticmethod
    def SetDataEcg(col_ecg,col_bpm,col_pred,id,ecg,bpm,pred):
        if id:
            if ecg:
                ecg_restruc = reestructurar_cadena(ecg, id)
                result = col_ecg.insert_one(ecg_restruc)
            if bpm:
                bpm_restruc = reestructurar_cadena(bpm, id)
                result = col_bpm.insert_one(bpm_restruc)
            if pred:
                pred_restruc = reestructurar_cadena(pred, id)
                result = col_pred.insert_one(pred_restruc)
            return True
        else:
            return False       