from ..config import REMEDIES,DEFAULT_REMEDY


def get_remedy_for_class(predicted_class:str)->dict:
    if "___" in predicted_class:
        plant_name,condition=predicted_class.split('___')
        plant_name=plant_name.replace("_",'').strip().title()
        condition=condition.replace('_','').strip().title()
        ishealthy='healthy' in condition.lower()
    else:
        plant_name='Unknown'
        condition='unknown'
        ishealthy='unknown'


    remedy_data=None
    for k,v in REMEDIES.items():
        if k==predicted_class:
            remedy_data=v
            break

    if remedy_data==None:
        remedy_data=DEFAULT_REMEDY

    return {
        "Plant":plant_name,
        "Condition":condition,
        "Is_Healthy":ishealthy,
        "Disease":remedy_data['disease'],
        "Action":remedy_data['actions']
    }